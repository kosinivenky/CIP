pipeline {
    agent any
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
        timeout(time: 1, unit: 'HOURS')
    }
    
    environment {
        PROJECT_NAME = 'CIP'
        BUILD_TIMEOUT = '60'
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "Checking out code from ${GIT_BRANCH}"
                }
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                script {
                    echo "Building ${PROJECT_NAME}..."
                    // Add your build commands here
                    // Example: sh 'npm install' or 'maven clean package'
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    echo "Running tests..."
                    // Add your test commands here
                    // Example: sh 'npm test' or 'maven test'
                }
            }
        }
        
        stage('Code Quality Analysis') {
            steps {
                script {
                    echo "Running code quality analysis..."
                    // Add SonarQube or other analysis tools
                    // Example: sh 'sonar-scanner'
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                script {
                    echo "Running security scan..."
                    // Add security scanning tools
                    // Example: sh 'trivy scan .'
                }
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                script {
                    echo "Deploying ${PROJECT_NAME}..."
                    // Add your deployment commands here
                    // Example: sh 'docker push' or deployment scripts
                }
            }
        }
        
        stage('Notifications') {
            steps {
                script {
                    echo "Sending notifications..."
                    // Add notification logic here
                }
            }
        }
    }
    
    post {
        always {
            echo "Pipeline execution completed"
            cleanWs()
        }
        success {
            echo "✓ Pipeline succeeded"
        }
        failure {
            echo "✗ Pipeline failed"
        }
        unstable {
            echo "⚠ Pipeline is unstable"
        }
    }
}
