
pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {
        stage('Check Environment') {
            steps {
                sh 'python3 --version'
                sh 'git --version'
            }
        }

        stage('Create Python Environment') {
            steps {
                sh 'python3 -m venv .venv'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '.venv/bin/python -m pip install -r requirements.txt'
            }
        }

        stage('Run Pytest') {
            steps {
                sh '.venv/bin/python -m pytest -v --junitxml=test-results/results.xml'
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true,
                  testResults: 'test-results/results.xml'
        }

        success {
            echo 'ShopFlow DataOps : BUILD SUCCESS !'
        }

        failure {
            echo 'ShopFlow DataOps : BUILD FAILED.'
        }
    }
}
