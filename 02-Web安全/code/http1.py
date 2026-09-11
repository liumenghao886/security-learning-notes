import requests

resp = requests.get("https://www.baidu.com")
resp.encoding = "utf-8"

print("===== 我发出的请求头 =====")
print(resp.request.headers)

print("\n===== 状态码 =====")
print(resp.status_code)

print("\n===== 服务器返回的响应头 =====")
print(resp.headers)
