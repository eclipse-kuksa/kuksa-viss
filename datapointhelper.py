
from kuksa_client.grpc import Datapoint
''' {
                "action": "get",
                "requestId": "8756",
                “data”:{“path”:”Vehicle.Drivetrain.InternalCombustionEngine/RPM”,
                        “dp”:{“value”:”2372”, “ts”:”2020-04-15T13:37:00Z”}
                       }
              '''


def populate_datapoints(data_from_db: "dict[str, Datapoint]"):
    data = {}  # VISSv2 a bit buggy, this is an object/dict for single paths, and array otherwise

    for path, dp in data_from_db.items():
        if dp is None:
            print(f"No data for {path}, skipping")
            continue
        data["path"] = path
        data["dp"] = {}
        data["dp"]["ts"] = dp.timestamp.isoformat()
        data["dp"]["value"] = dp.value

    return data
