# Challenge App - FastAPI con CI/CD en AWS

API REST para almacenamiento de documentos JSON con autenticación, balanceo de carga y despliegue automático en múltiples instancias EC2 usando GitHub Actions y Amazon ECR.


## Arquitectura

- **API**: FastAPI con Gunicorn
- **Container Registry**: Amazon ECR  
- **Deployment**: Múltiples EC2 con Docker Compose
- **CI/CD**: GitHub Actions con OIDC
- **Automatización**: AWS Systems Manager (SSM)
- **Alta Disponibilidad**: Deploy simultáneo en 2 instancias EC2

## Flujo de CI/CD

### 1. **Pull Request Workflow** (Validación)
- Build de la imagen Docker
- Análisis de seguridad con Trivy
- Linting y validación de código
- No hace push ni deploy

### 2. **Main Branch Workflow** (Deploy)
- Build y push de imagen a ECR con tag `vN`
- Deploy automático a TODAS las EC2s configuradas
- Actualización sin downtime
- Health checks post-deploy

## Estructura del Proyecto

```
.
├── .github/
│   └── workflows/
│       ├── deploy-to-ecr.yml      # Deploy a producción
│       └── pr-validation.yml      # Validación en PRs
├── docker/
│   ├── Dockerfile                 # Imagen de la aplicación
│   ├── main.py                   # API FastAPI
│   ├── requirements.txt          # Dependencias Python
│   └── docker-compose.yml        # Para desarrollo local
├── pruebas/
│   ├── test_api.py               # Tests de la API
│   └── test_balanceo.py          # Tests de balanceo
└── README.md
```

## Configuración Inicial

### 1. AWS ECR
```bash
# Crear repositorio ECR
aws ecr create-repository --repository-name challenge-app --region us-east-1
```

### 2. GitHub Secrets y Variables

#### Variables (Settings → Secrets and variables → Actions → Variables):
- `AWS_REGION`: Región de AWS (ej: `us-east-1`)
- `ECR_REPOSITORY`: Nombre del repositorio ECR (ej: `challenge-app`)
- `EC2_INSTANCE_IDS`: IDs de las instancias separados por coma (ej: `i-abc123,i-def456`)

#### Secrets:
- `AWS_ROLE_ARN`: ARN del rol para GitHub OIDC

### 3. Configuración OIDC en AWS

1. Crear Identity Provider en IAM:
   - Provider URL: `https://token.actions.githubusercontent.com`
   - Audience: `sts.amazonaws.com`

2. Crear rol con política de confianza:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:YOUR_ORG/YOUR_REPO:*"
        }
      }
    }
  ]
}
```

3. Políticas necesarias para el rol:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:PutImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ssm:SendCommand",
        "ssm:GetCommandInvocation",
        "ssm:ListCommandInvocations"
      ],
      "Resource": [
        "arn:aws:ssm:*:*:document/AWS-RunShellScript",
        "arn:aws:ec2:*:*:instance/*"
      ]
    }
  ]
}
```

### 4. Configuración EC2 (Ambas instancias)

Cada instancia EC2 debe tener:
- Docker y Docker Compose instalados
- SSM Agent activo
- Rol con políticas:
  - `AmazonSSMManagedInstanceCore`
  - Acceso a ECR (pull)

```bash
# Verificar SSM Agent
sudo systemctl status amazon-ssm-agent

# Si no está activo
sudo systemctl start amazon-ssm-agent
sudo systemctl enable amazon-ssm-agent
```

## API Endpoints

### Endpoints públicos
```bash
# Health check
curl http://EC2_IP/health

# Leer JSON
curl http://EC2_IP/json/mi-id
```

### Endpoints protegidos
```bash
# Crear JSON
curl -X POST http://EC2_IP/json \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"id": "test", "data": {"key": "value"}}'

# Actualizar JSON
curl -X PUT http://EC2_IP/json/test \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"key": "new value"}'

# Eliminar JSON
curl -X DELETE http://EC2_IP/json/test \
  -H "Authorization: Bearer ${API_TOKEN}"
```

## Proceso de Deploy

### Deploy Automático (Recomendado)

1. Crear una rama para tu feature:
```bash
git checkout -b feature/mi-cambio
```

2. Hacer cambios y commit:
```bash
git add .
git commit -m "feat: agregar nueva funcionalidad"
git push origin feature/mi-cambio
```

3. Crear Pull Request en GitHub
   - Se ejecutarán validaciones automáticas
   - Build de prueba
   - Análisis de seguridad con Trivy

4. Al aprobar y hacer merge a main:
   - Se construye nueva imagen con tag `vN` 
   - Se pushea a ECR
   - Se despliega automáticamente a TODAS las EC2s configuradas
   - Health check en cada instancia

### Verificar balanceo de carga
```bash
cd pruebas
python3 test_balanceo.py
```

---

👤 **Autor**: Hermes Vargas  
📧 **Email**: hermes.vargas@cloudhesive.com