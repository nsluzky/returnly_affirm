/* The script runs a single unittest
* Parameters:
* BRANCH - Branch in git repository
* COMMAND_LINE - set PARAMS, set PYTHONPATH, run test
* NAME - name to be set to the build
* PARENTS_WORKSPACE - location of the parents workspace to copy the log
* RESTART_IF_FAILED - If True, failed test would be restarted
* */

/**
 * Copy log file to main job
 * @param result
 */
string log = "test.log"
string result = ''

node('master') {
    sh 'rm -rf *'
    sh 'touch ' + log
    echo params.COMMAND_LINE
    currentBuild.displayName += (" " + params.NAME)
    lock(label: 'job', quantity: 1, variable: 'jobName') {
        sh 'git clone https://github.com/vsluzky23/CommonAutomationUi.git'
        if (params.BRANCH != 'master') {
            sh 'cd CommonAutomationUi; git checkout ' + params.BRANCH + '; cd ..'
        }
        try {
            sh params.COMMAND_LINE
            result = 'passed'
        } catch (Exception exeption) {
            result = 'failed'
            if (params.RESTART_IF_FAILED.equals("True")) {
                try {
                    sh params.COMMAND_LINE
                    result = 'passed_on_rerun'
                } catch (Exception exception2) {
                    result = "failed_twice"
                }
            }
        } finally {
            sh "echo " + env["BUILD_URL"] + " >> " + log
            try {
                archiveArtifacts artifacts: "screenshots/*.png"
            } catch (Exception e) {
                print('Exception while archiving screenshots ' + e.toString())
            }
            string name = params.NAME
            if (params.PARENTS_WORKSPACE != "")
                sh "cp " + log + " " + params.PARENTS_WORKSPACE + "/" + name + "_" + result + ".log"
            result = "<" + env["BUILD_URL"] + "/console|" + name + " " + result + ">"
            if (result.contains("failed"))
                throw new RuntimeException((result))
            sh 'rm -rf *'
        }
    }
}
