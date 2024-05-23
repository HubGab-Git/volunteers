docker build -t ${ecr_url}:${image_tag} --platform linux/amd64 --build-arg FUNCTION_NAME=${name} .

aws ecr get-login-password --region ${region} | docker login --username AWS --password-stdin ${ecr_reg}

docker push ${ecr_url}:${image_tag}