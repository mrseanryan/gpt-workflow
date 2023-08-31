echo "Test USAGE"
./go.sh

echo .
echo "Test parsing DOT"
./go.sh parse ../../dot/example-output/dot_graph_1.dot

echo .
echo "Test building DOT"
./go.sh create-example-dot
