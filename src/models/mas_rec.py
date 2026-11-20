"""Readable PyTorch implementation of the MAS-Rec rating model."""

from __future__ import annotations

import torch
from torch import nn


class BidirectionalCoAttention(nn.Module):
    """Let the pooled user and item representations attend to each other."""

    def __init__(self, embedding_dim: int = 320, num_heads: int = 8) -> None:
        super().__init__()
        self.user_to_item = nn.MultiheadAttention(
            embedding_dim, num_heads, batch_first=True
        )
        self.item_to_user = nn.MultiheadAttention(
            embedding_dim, num_heads, batch_first=True
        )

    def forward(self, user_vector: torch.Tensor, item_vector: torch.Tensor) -> torch.Tensor:
        user_sequence = user_vector.unsqueeze(1)
        item_sequence = item_vector.unsqueeze(1)
        user_context, _ = self.user_to_item(
            user_sequence, item_sequence, item_sequence, need_weights=False
        )
        item_context, _ = self.item_to_user(
            item_sequence, user_sequence, user_sequence, need_weights=False
        )
        return torch.cat([user_context[:, 0], item_context[:, 0]], dim=-1)


class MASRec(nn.Module):
    """Two fine-tuned BERT towers, ID embeddings, and co-attention."""

    def __init__(
        self,
        *,
        num_users: int,
        num_items: int,
        user_encoder: nn.Module,
        item_encoder: nn.Module,
        text_hidden_size: int = 768,
        id_embedding_size: int = 64,
        num_heads: int = 8,
    ) -> None:
        super().__init__()
        self.user_embedding = nn.Embedding(num_users, id_embedding_size)
        self.item_embedding = nn.Embedding(num_items, id_embedding_size)
        self.user_encoder = user_encoder
        self.item_encoder = item_encoder
        self.text_projection = nn.Sequential(
            nn.Linear(text_hidden_size, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
        )
        feature_size = id_embedding_size + 256
        self.co_attention = BidirectionalCoAttention(feature_size, num_heads)
        self.rating_head = nn.Sequential(
            nn.Linear(feature_size * 2, 256), nn.ReLU(), nn.Linear(256, 1)
        )

    @staticmethod
    def _pooled_cls(encoder, input_ids, attention_mask):
        return encoder(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state[:, 0]

    def forward(
        self,
        *,
        user_id,
        item_id,
        input_ids_user,
        attention_mask_user,
        input_ids_item,
        attention_mask_item,
        labels=None,
    ):
        user_text = self.text_projection(
            self._pooled_cls(self.user_encoder, input_ids_user, attention_mask_user)
        )
        item_text = self.text_projection(
            self._pooled_cls(self.item_encoder, input_ids_item, attention_mask_item)
        )
        user_feature = torch.cat([self.user_embedding(user_id), user_text], dim=-1)
        item_feature = torch.cat([self.item_embedding(item_id), item_text], dim=-1)
        prediction = self.rating_head(
            self.co_attention(user_feature, item_feature)
        ).squeeze(-1)
        result = {"logits": prediction}
        if labels is not None:
            result["loss"] = nn.functional.mse_loss(prediction, labels.float())
        return result

