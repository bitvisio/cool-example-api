
# Cool API Template Documentation

This repository provides a template for building and deploying FastAPI-based applications with Kubernetes and CI/CD pipelines. It includes a pre-configured and structured project layout, Kubernetes manifests, and GitHub Actions workflows for automated deployments.

---

## **Project Structure**

```
.
├── .github 
│   └── workflows                       # CI/CD workflows for GitHub Actions
│       ├── deploy_local.yml            # Workflow for local deployment
│       ├── deploy_qa.yml               # Workflow for QA environment
│       └── deploy_prod.yml             # Workflow for production environment
├── k8s                                 # Kubernetes manifests
│   ├── base                            # Base manifests for Kustomize
│   │   ├── deployment.yaml             # Base deployment configuration
│   │   ├── service.yaml                # Base service configuration
│   │   └── kustomization.yaml          # Kustomize base configuration
│   └── overlays                        # Environment-specific overlays
│       ├── qa
│       │   ├── kustomization.yaml      # QA-specific Kustomize configuration
│       │   ├── deployment-patch.yaml   # QA-specific deployment patch
│       │   ├── ingress.yaml            # QA-specific Ingress configuration
│       │   └── service-patch.yaml      # QA-specific service patch
│       └── prod
│           ├── kustomization.yaml      # Production-specific Kustomize configuration
│           ├── deployment-patch.yaml   # Production-specific deployment patch
│           ├── ingress.yaml            # Production-specific Ingress configuration
│           └── service-patch.yaml      # Production-specific service patch
├── src                                 # Source code
│   ├── api                             # API routers
│   ├── model                           # Data models
│   └── service                         # Business logic
├── test                                # Unit and integration tests
│   ├── api                             # API tests
│   └── service                         # Service tests
├── main.py                             # FastAPI application entry point
├── Dockerfile                          # Dockerfile for building the application image
├── pyproject.toml                      # Project metadata and dependencies
├── requirements.txt                    # Application dependencies
├── dev-requirements.txt                # Development dependencies
└── README.md                           # Project documentation
```

---

## **Features**

- **FastAPI Framework**: A web framework for building APIs with Python.
- **Kubernetes Deployment**: Includes manifests for deploying the application to Kubernetes using Kustomize.
- **CI/CD Pipelines**: Automated workflows for testing, building, and deploying the application to local, QA, and production environments.
- **Ingress Support**: Configured for domain-based routing with environment-specific Ingress rules.
- **Unit and Integration Tests**: Comprehensive test coverage for API endpoints and business logic.

---

## **Getting Started**

### **1. Prerequisites**
- Python 3.11 or higher
  
Optional:
- Docker (for running the application locally)
- Kubernetes (e.g., Minikube, Kind, for testing deployment to Kubernetes locally) 
- kubectl and Kustomize (for testing deployment to Kubernetes locally)
- GitHub Local Actions (for testing CI/CD workflows locally)

---

### **5. Running Tests**

**Run API tests**:
   ```sh
   PYTHONPATH=./ pytest test/api/test_message_api.py
   ```

**Run service tests**:
   ```sh
   PYTHONPATH=./ pytest test/service/test_message_service.py
   ```

---

### **2. Running the Application Locally**

1. **Install dependencies**:
   ```sh
   python3 -m pip install -r dev-requirements.txt
   ```

2. **Run the application**:
   ```sh
   uvicorn main:app --host 0.0.0.0 --port 5000
   ```

3. **Access the API documentation**:
   - Swagger UI: [http://localhost:5000/docs](http://localhost:5000/docs)
   - ReDoc: [http://localhost:5000/redoc](http://localhost:5000/redoc)

---

### **3. Running the Application with Docker**

1. **Build the Docker image**:
   ```sh
   docker build -t Cool-example-api:1.0.0 .
   ```

2. **Run the Docker container**:
   ```sh
   docker run --name Cool-example-api -p 5000:5000 -t Cool-example-api:1.0.0
   ```

3. **Access the API documentation**:
   - Swagger UI: [http://localhost:5000/docs](http://localhost:5000/docs)

---

### **4. Deploying to Kubernetes**

#### **Apply the base manifests**:
   ```sh
   kubectl apply -k k8s/base
   ```

#### **Apply environment-specific overlays**:
   - QA:
     ```sh
     kubectl apply -k k8s/overlays/qa
     ```
   - Production:
     ```sh
     kubectl apply -k k8s/overlays/prod
     ```


---


## **CI/CD Pipelines**

### **Local Deployment**
- Triggered manually via GitHub Local Actions.
- Runs tests, builds the Docker image, and deploys to the local environment.

### **QA Deployment**
- Triggered on pushes to the `test` branch.
- Runs tests, builds the Docker image, pushes image to Jfrog Artifactory and deploys to the QA environment.

### **Production Deployment**
- Triggered on pushes to the `main` branch.
- deploys to the production environment.

---

## **Kubernetes Configuration**

### **Base Manifests**
- `deployment.yaml`: Defines the application deployment.
- `service.yaml`: Exposes the application within the cluster.

### **Environment-Specific Overlays**
- **QA**:
  - `deployment-patch.yaml`: Sets replicas to 1 and environment to `qa`.
  - `ingress.yaml`: Configures Ingress for `qa.Cool-api.example.fi`.
- **Production**:
  - `deployment-patch.yaml`: Sets replicas to 2 and environment to `production`.
  - `ingress.yaml`: Configures Ingress for `prod.Cool-api.example.fi`.

---
