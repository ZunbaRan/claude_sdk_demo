
claude mcp add -s user zai-mcp-server --env Z_AI_API_KEY=2c1aafa6fec3870a1b58ce4110103563.RDKI6qfuATJ7gb2k -- npx -y "@z_ai/mcp-server"


claude mcp add -s user -t http web-search-prime https://open.bigmodel.cn/api/mcp/web_search_prime/mcp --header "Authorization: Bearer 2c1aafa6fec3870a1b58ce4110103563.RDKI6qfuATJ7gb2k"


claude mcp add -s user -t http web-reader https://open.bigmodel.cn/api/mcp/web_reader/mcp --header "Authorization: Bearer 2c1aafa6fec3870a1b58ce4110103563.RDKI6qfuATJ7gb2k"

claude mcp add --transport http context7 https://mcp.context7.com/mcp --header "CONTEXT7_API_KEY: ctx7sk-f6cd2808-7613-4a96-9002-401a187d2ae6"