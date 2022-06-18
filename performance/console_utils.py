def get_usage_bar(usage, value, size=2, limit=100, typeof="%"):
    carga = ''
    for i in range((size - 1), int(usage), size):
        carga += "#"
    for j in range(int(usage), limit, size):
        carga += "."
    return "[" + carga + " " + str(value) + " " + typeof + "]"
