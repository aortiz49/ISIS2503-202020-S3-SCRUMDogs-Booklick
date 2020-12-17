pipeline {
  agent {
    docker {
      image 'python:3.5.1'
    }

  }
  stages {
    stage('Install Packages') {
      steps {
        sh 'pip install --upgrade pip'
      }
    }

    stage('Build') {
      steps {
        echo 'HELLO WORLD'
      }
    }

  }
}