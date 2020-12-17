pipeline {
  agent any
  stages {
    stage('Install Packages') {
      steps {
        sh 'sudo pip install --upgrade pip'
      }
    }

    stage('Build') {
      steps {
        echo 'HELLO WORLD'
      }
    }

  }
}