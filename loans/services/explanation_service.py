from functools import lru_cache

import numpy as np
import pandas as pd
import shap

from .ml_service import (
    build_model_input,
    load_primary_model,
)


@lru_cache(maxsize=1)
def get_explainer():
    pipeline = load_primary_model()

    model = pipeline.named_steps["model"]

    return shap.TreeExplainer(model)


def get_feature_mapping(preprocessor):
    numeric_features = list(
        preprocessor.transformers_[0][2]
    )

    categorical_features = list(
        preprocessor.transformers_[1][2]
    )

    encoder = preprocessor.named_transformers_["cat"]

    original_features = numeric_features.copy()

    for feature, categories in zip(
        categorical_features,
        encoder.categories_
    ):
        original_features.extend(
            [feature] * len(categories)
        )

    return original_features


def explain_application(application, top_n=10):
    pipeline = load_primary_model()

    preprocessor = pipeline.named_steps[
        "preprocessor"
    ]

    model_input = build_model_input(
        application
    )

    transformed = preprocessor.transform(
        model_input
    )

    feature_names = (
        preprocessor.get_feature_names_out()
    )

    transformed_df = pd.DataFrame(
        transformed,
        columns=feature_names
    )

    explainer = get_explainer()

    shap_result = explainer(
        transformed_df
    )

    original_features = get_feature_mapping(
        preprocessor
    )

    shap_values = shap_result.values[0]

    local_explanation = pd.DataFrame({
        "feature": original_features,
        "shap_value": shap_values,
    })

    local_explanation = (
        local_explanation
        .groupby(
            "feature",
            as_index=False
        )["shap_value"]
        .sum()
    )

    raw_values = (
        model_input.iloc[0].to_dict()
    )

    local_explanation["value"] = (
        local_explanation["feature"]
        .map(raw_values)
    )

    local_explanation[
        "absolute_shap"
    ] = np.abs(
        local_explanation["shap_value"]
    )

    local_explanation["direction"] = (
        local_explanation[
            "shap_value"
        ].apply(
            lambda value:
            "Toward Approved"
            if value > 0
            else "Toward Rejected"
        )
    )

    local_explanation = (
        local_explanation
        .sort_values(
            "absolute_shap",
            ascending=False
        )
        .head(top_n)
    )

    explanation = []

    for _, row in local_explanation.iterrows():
        explanation.append({
            "feature": row["feature"],
            "value": row["value"],
            "shap_value": round(
                float(row["shap_value"]),
                4
            ),
            "direction": row["direction"],
        })

    return explanation