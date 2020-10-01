import io

stream = io.BytesIO(content)
data = JSONParser().parse(stream)