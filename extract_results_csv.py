import json
import csv
results_json_path = "bundle_map_results.json"

with open(results_json_path) as f:
    results_data = json.load(f)

data = []

with open("bundle_map_results.csv", "w") as out_f:
    writer = csv.writer(out_f)
    writer.writerow(
        [
            "experiment",
            "backbone",
            "img_size",
            "mpixel",
            "total_s_mean",
            "total_s_std",
            "infer_s_mean",
            "infer_s_std",
            "postprocess_s_mean",
            "postprocess_s_std",
            "preprocess_s_mean",
            "preprocess_s_std",
            "serialize_s_mean",
            "serialize_s_std",
        ]
    )
    for experiment, models_dict in results_data.items():
        for model_size, bundles in models_dict.items():
            for bundle in bundles:
                row_dict = {
                    "experiment": experiment,
                    "backbone": model_size,
                    "size": bundle["size"],
                    "mpixel": bundle["mpixel"],
                    "total_s_mean": bundle["latency_results"]["total_s"]["mean"],
                    "total_s_std": bundle["latency_results"]["total_s"]["std"],
                    "infer_s_mean": bundle["latency_results"]["infer_s"]["mean"],
                    "infer_s_std": bundle["latency_results"]["infer_s"]["std"],
                    "postprocess_s_mean": bundle["latency_results"]["postprocess_s"]["mean"],
                    "postprocess_s_std": bundle["latency_results"]["postprocess_s"]["std"],
                    "preprocess_s_mean": bundle["latency_results"]["preprocess_s"]["mean"],
                    "preprocess_s_std": bundle["latency_results"]["preprocess_s"]["std"],
                    "serialize_s_mean": bundle["latency_results"]["serialize_s"]["mean"],
                    "serialize_s_std": bundle["latency_results"]["serialize_s"]["std"],
                }

                writer.writerow(row_dict.values())




