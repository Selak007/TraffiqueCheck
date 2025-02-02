import kagglehub

# Download latest version
path = kagglehub.dataset_download("fahaddalwai/cctvfootagevideo")

print("Path to dataset files:", path)