import kagglehub

# Download latest version
path = kagglehub.model_download("farhaanaliv/weights/tensorFlow2/default")

print("Path to model files:", path)