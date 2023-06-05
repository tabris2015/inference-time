import json
import logging

import numpy as np

from fire import Fire

import avi_io
from avi_inference.inference_model import InferenceModel

_LOGGER = logging.getLogger(__name__)


def start() -> None:
    setup_logs()
    Fire(main)


def main(config_path: str, iterations: int) -> None:
    _LOGGER.info(f"Reading bundles to test from {config_path}")
    
    bundles_data = read_configs(config_path)
    bundles_root = bundles_data.pop("bundles_root")
    for experiment_type, models_dict in bundles_data.items():
        _LOGGER.info(f"Starting inference test for {experiment_type}...")
        for model_size, bundles in models_dict.items():
            _LOGGER.info(f"Running {model_size} bundles")
            for bundle in bundles:
                _LOGGER.info(f"Loading bundle {bundle['bundle']} with image size {bundle['size']}")

                bundle_path = f"{bundles_root}{experiment_type}/{bundle['bundle']}"
                _LOGGER.info(f"Bundle location: {bundle_path}")
                model = InferenceModel.from_bundle(bundle_path)

                image = avi_io.read_image(bundle["image"])

                results = avg_results(model, image, iterations=iterations)

                _LOGGER.info(f"Results for {experiment_type}, {model_size}, {bundle['size']}: {results}")
                bundle.update({"latency_results": results})

    with open(f"bundle_map_results.json", "w+") as dest:
        json.dump(bundles_data, dest, indent=2)


def get_mean_std(latencies):
    infer_list = np.array([l.infer_s for l in latencies])
    postprocess_list = np.array([l.postprocess_s for l in latencies])
    preprocess_list = np.array([l.preprocess_s for l in latencies])
    serialize_list = np.array([l.serialize_s for l in latencies])
    total_list = np.array([l.infer_s + l.postprocess_s + l.preprocess_s + l.serialize_s for l in latencies])

    return {
        "infer_s": {"std": np.std(infer_list), "mean": np.mean(infer_list)},
        "postprocess_s": {"std": np.std(postprocess_list), "mean": np.mean(postprocess_list)},
        "preprocess_s": {"std": np.std(preprocess_list), "mean": np.mean(preprocess_list)},
        "serialize_s": {"std": np.std(serialize_list), "mean": np.mean(serialize_list)},
        "total_s": {"std": np.std(total_list), "mean": np.mean(total_list)},
    }


def avg_results(model, image, iterations=100) -> dict:
    # throw away first inference for loading
    print("ignore first")
    model.predict([image], trim_results_for_inference_apps=True)
    latencies = []
    for _ in range(iterations):
        latencies.append(model.predict([image], trim_results_for_inference_apps=True)[0].latency)
        print(".", end=" ")

    print("fin")
    results = get_mean_std(latencies)

    return results


def setup_logs():
    logging.basicConfig(level="DEBUG")
    logging.getLogger("boto3").setLevel(logging.CRITICAL)
    logging.getLogger("botocore").setLevel(logging.CRITICAL)
    logging.getLogger("nose").setLevel(logging.CRITICAL)
    logging.getLogger("s3transfer").setLevel(logging.CRITICAL)
    logging.getLogger("urllib3").setLevel(logging.CRITICAL)
    logging.getLogger("matplotlib").setLevel(logging.CRITICAL)
    logging.getLogger("PIL").setLevel(logging.CRITICAL)
    logging.getLogger("avi_inference").setLevel(logging.CRITICAL)



def read_configs(config_path: str) -> dict:
    with open(config_path, "r") as f:
        data = json.load(f)

    return data


if __name__ == "__main__":
    start()
