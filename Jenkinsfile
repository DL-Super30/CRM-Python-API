pipeline {
    agent any // This sets the pipeline to run on any available Jenkins agent

    stages {
        stage('Containers') {
            steps {
                script {
                    // List Docker containers
                    sh 'docker container ls'
                }
            }
        }
        stage('Build') {
            steps {
                script {
                    // Change directory to skill-capital-crm and build Docker image
                        sh 'docker build -t fastapi .'
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    // Stop and remove any existing container with the same name
                    sh 'docker container stop django || true'
                    sh 'docker container rm django || true'

                    // Run Docker container
                    sh 'docker run -d --name django -p 8000:8000 fastapi'
                }
            }
        }
        stage('Output') {
            steps {
                echo 'Successfully deployed in Jenkins'
            }
        }
    }
}
