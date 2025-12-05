#! /bin/bash
pushd () {
    command pushd "$@" > /dev/null
}
popd () {
    command popd "$@" > /dev/null
}

echo "Generating Python gRPC code"
ROOT_DIR="$(git rev-parse --show-toplevel)"
pushd "$ROOT_DIR/api/generated"
source ../venv/bin/activate
python -m grpc_tools.protoc \
    -I ../../protos \
    --python_out=. \
    --pyi_out=. \
    --grpc_python_out=. \
    ../../protos/*.proto

echo "Generating Typescript gRPC code"
pushd "$ROOT_DIR/web"
protoc \
  --plugin="protoc-gen-ts_proto=./node_modules/.bin/protoc-gen-ts_proto" \
  --ts_proto_out=./generated \
  --ts_proto_opt="esModuleInterop=true,forceLongToString=true,outputServices=grpc-js" \
  -I ../protos/ \
  ../protos/equity.proto

popd
popd
