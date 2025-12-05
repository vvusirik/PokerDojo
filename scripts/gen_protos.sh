#! /bin/bash
pushd () {
    command pushd "$@" > /dev/null
}
popd () {
    command popd "$@" > /dev/null
}

echo "Generating Python gRPC code"
ROOT_DIR="$(git rev-parse --show-toplevel)"
OUT_DIR="$ROOT_DIR/api/generated"
pushd "$ROOT_DIR/api/"
source ./venv/bin/activate
python -m grpc_tools.protoc \
    --python_out=$OUT_DIR \
    --pyi_out=$OUT_DIR \
    --grpc_python_out=$OUT_DIR \
    -I $ROOT_DIR/protos $ROOT_DIR/protos/*.proto

echo "Generating Typescript gRPC code"
OUT_DIR="$ROOT_DIR/web/generated"
pushd "$ROOT_DIR/web"
protoc -I=$ROOT_DIR/protos $ROOT_DIR/protos/*.proto \
  --ts_out=import_style=commonjs:$OUT_DIR \
  --grpc-web_out=import_style=commonjs,mode=grpcwebtext:$OUT_DIR
popd
popd

