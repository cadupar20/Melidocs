try:
    # FastAPI's jsonable_encoder handles converting various non-JSON types,
    # such as datetime between JSON types and native Python types.
    from fastapi.encoders import jsonable_encoder
except Exception as e:
    print("Some modules are missing {}".format(e))

