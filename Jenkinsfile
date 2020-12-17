pipeline {
  agent {
    docker {
      image 'python:3.5.1'
    }

  }
  stages {
    stage('Install Packages') {
      steps {
        sh 'sudo pip install -r "requirements.txt"'
      }
    }

    stage('Build') {
      steps {
        echo 'HELLO WORLD'
      }
    }

  }
}