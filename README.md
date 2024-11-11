# ICD Code Generator using Ollama and Streamlit on AWS EC2

This project implements an ICD (International Classification of Diseases) code generation system using a custom language model through Ollama, deployed on AWS EC2 using Docker and presented via a Streamlit interface.

## Table of Contents
- [System Architecture](#system-architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Docker Setup](#docker-setup)
- [AWS EC2 Configuration](#aws-ec2-configuration)
- [Application Deployment](#application-deployment)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Security Considerations](#security-considerations)
- [Contributing](#contributing)
- [License](#license)

## System Architecture

The system consists of several components:
- Custom Language Model (deployed via Ollama)
- Docker container for model isolation
- Streamlit web interface
- AWS EC2 instance for hosting
- Network configuration for secure access

## Prerequisites

### Local Development
- Python 3.8+
- Docker Desktop
- Git
- AWS Account
- Basic understanding of terminal/command line

### Required Python Packages
```bash
streamlit>=1.24.0
ollama>=0.1.0
python-dotenv>=0.19.0
requests>=2.28.0
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Vimlesh-17/ICD10-llama3.2.git

```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Docker Setup

1. Build the custom model image:
```bash
docker build -t icd-model-image -f Dockerfile.model .
```

2. Build the application image:
```bash
docker build -t icd-app-image -f Dockerfile.app .
```

3. Create a Docker network:
```bash
docker network create icd-network
```

4. Run the containers:
```bash
docker run -d --name model-container --network icd-network icd-model-image
docker run -d --name app-container --network icd-network -p 8501:8501 icd-app-image
```

## AWS EC2 Configuration

1. Launch EC2 Instance:
   - Choose Ubuntu Server 22.04 LTS
   - Recommended: t2.large or better
   - Storage: Minimum 30GB EBS
   - Configure Security Group:
     ```
     HTTP (80) - Source: 0.0.0.0/0
     HTTPS (443) - Source: 0.0.0.0/0
     Custom TCP (8501) - Source: 0.0.0.0/0
     SSH (22) - Source: Your IP
     ```

2. Connect to EC2:
```bash
chmod 400 your-key-pair.pem
ssh -i your-key-pair.pem ubuntu@your-ec2-ip
```

3. Install Dependencies:
```bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker ubuntu
```

## Application Deployment

1. Transfer files to EC2:
```bash
scp -i your-key-pair.pem -r ./icd-code-generator ubuntu@your-ec2-ip:~/
```

2. Deploy on EC2:
```bash
cd icd-code-generator
docker-compose up -d
```

3. Configure SSL (Optional but recommended):
```bash
sudo apt-get install certbot
sudo certbot certonly --standalone -d your-domain.com
```

## Usage

1. Access the application:
```
http://your-ec2-ip:8501
```
or if SSL configured:
```
https://your-domain.com
```

2. Using the Interface:
   - Enter medical text in the input field
   - Click "Generate ICD Codes"
   - View generated codes and descriptions
   - Export results if needed

## Troubleshooting

### Common Issues and Solutions

1. Docker Container Issues:
```bash
# Check container logs
docker logs app-container
docker logs model-container

# Restart containers
docker-compose restart
```

2. Model Loading Issues:
```bash
# Verify model files
docker exec -it model-container ls /app/model

# Check Ollama logs
docker exec -it model-container cat /var/log/ollama.log
```

3. Network Issues:
```bash
# Test network connectivity
docker network inspect icd-network

# Verify ports
netstat -tulpn | grep LISTEN
```

## Security Considerations

1. AWS Security:
   - Use IAM roles with minimal permissions
   - Keep security groups restricted
   - Regularly update security patches

2. Application Security:
   - Implement rate limiting
   - Use HTTPS
   - Sanitize user inputs
   - Regular security audits

3. Data Protection:
   - Encrypt sensitive data
   - Regular backups
   - Comply with healthcare data regulations

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Contact

For support or queries, please contact:
- Email: vimleshc7317@gmail.com
- Issue Tracker: GitHub Issues

## Acknowledgments

- Ollama team for the model serving framework
- Streamlit team for the web interface framework
- AWS for cloud infrastructure
```
