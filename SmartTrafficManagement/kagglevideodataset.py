import kagglehub

# Download latest version
path = kagglehub.dataset_download("aalborguniversity/aau-rainsnow")

print("Path to dataset files:", path)