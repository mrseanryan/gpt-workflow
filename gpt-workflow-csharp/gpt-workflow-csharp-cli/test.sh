echo "Test USAGE"
./go.sh

echo .
echo "Test parsing DOT"
./go.sh parse ../../dot/example-output/dot_graph_1.dot

echo .
echo "Test building DOT"
./go.sh create-example-dot

echo .
echo "Test building DOT and sending it to web server to get Description"
./go.sh send-example-dot-to-describe

echo .
echo "Test send Natural Language to web server to get DOT and parse that"
./go.sh generate-dot-and-parse "Create a flow that makes a series of decisions about whether to recommend a job interview candidate."
