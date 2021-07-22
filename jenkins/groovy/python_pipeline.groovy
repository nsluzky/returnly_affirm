/* The script finds tests to run based on provided parameters and starts them
 * Parameters:
  * INCLUDE_TESTS - Regular expression to determine tests to include
  * SKIP_TESTS - Regular expression to specify tests to exclude (optional)
  * DRYRUN - If set, list of tests is determined, but not  started.
  * BRANCH - Branch in git repository
  * ADDITIONAL_ARBITRARY_PARAMETERS - Additional parameters that would be passed to the tests
  * RESTART_IF_FAILED - If True, failed test(s) would be restarted
  * */


/**
 * Return url of a thread build
 * @param job_name
 * @return
 */
def get_thread_url(job_name) {
    return Hudson.instance.getJob(job_name).getLastBuild().getAbsoluteUrl()
}

def test_files

def status = "passed"
node('master') {
    string workspace = pwd()
    string repo = 'CommonAutomationUi'
    int failed_threads = 0
    string html_log = ''
    currentBuild.displayName += (
            ' ' + params.BRANCH
                + ' Incl:' + params.INCLUDE_TESTS
            )
    if (params.SKIP_TESTS > '')
        currentBuild.displayName += (' Skip:' + params.SKIP_TESTS)
    if (params.DRYRUN == true)
        currentBuild.displayName += ' Dryrun'
    def TESTS = ""
    stage("Find tests to run") {
        sh 'rm -rf *'
        sh 'git clone https://github.com/vsluzky23/' + repo + '.git'
        if (params.BRANCH != 'master') {
            sh 'cd ' + repo + '; git checkout ' + params.BRANCH + '; cd ..'
        }
        def temp_file = "selected_tests"
        def all_files = "all_tests"
        sh 'find ' + repo + ' -name tc*.py > ' + all_files
        def grep_command = 'grep -E -i ".*' + params.INCLUDE_TESTS + '" ' + all_files
        if (params.SKIP_TESTS > '')
            grep_command += (' | grep -v -E ' + "'" + params.SKIP_TESTS) + "'"
        grep_command += (' > ' + temp_file)
        print('grep_command=' + grep_command)
        sh grep_command
        test_files = readFile(temp_file).split('\n')
        for (test in test_files) {
            TESTS += (',' + test)
            print(test)
        }
    }
    currentBuild.displayName += (' ' + test_files.size() + ' test(s)')
    if (test_files.size() < 1)
        throw new Exception("None tests to run were found; please review BRANCH and search parameters")

    stage('run_tests') {
        if (params.DRYRUN == true)
            return
        /************************* Validate parameters *************************/
        def animate = "True"
        if (params.ANIMATE == false)
            animate = "False"
        def save_screenshots = "True"
        if (params.SAVE_SCREENSHOTS == false)
            save_screenshots = "False"
        def execs = [:]
        for (def test_iter in test_files) {
            def test = test_iter
            string thread_item = test.substring(test.lastIndexOf("/") + 1, test.lastIndexOf("."))
            execs[thread_item] = {
                node('master') {
                    status = 'passed'
                    string command = 'export PARAMS="{'
                    command += ("'" + "animate" + "':" + animate + ",")
                    command += ("'" + "save_screenshots" + "':" + save_screenshots + ",")
                    if (params.ARBITRARY > '')
                        command += params.ARBITRARY
                    command += '}"'
                    // Set PYTHONPATH
                    command += ("; export PYTHONPATH=" + repo)
                    command += "; export PATH=$PATH:/usr/local/bin"
                    // Run Tests
                    command += ("; python3 " + test)
                    string thread = params.BRANCH + "_"
                    int from = test.indexOf("/tc")
                    int to = test.indexOf("_", from)
                    if (from > -1 && to > -1) {
                        thread += test.substring(from + 1, to)
                    } else
                        thread += test

                    try {
                        print('************** command=\n"' + command + '"')
                        result = build job: "RunOneTest", parameters: [
                                [$class: 'StringParameterValue', name: 'BRANCH', value: params.BRANCH],
                                [$class: 'StringParameterValue', name: 'COMMAND_LINE', value: command],
                                [$class: 'StringParameterValue', name: 'NAME', value: thread],
                                [$class: 'StringParameterValue', name: 'PARENTS_WORKSPACE',
                                 value : workspace],
                                [$class: 'BooleanParameterValue', name: 'RESTART_IF_FAILED',
                                 value : params.RESTART_IF_FAILED]
                        ]
                    } catch (Exception e) {
                        failed_threads += 1
                        status = 'failed'
                    } finally {
                        if (status != 'passed')
                            throw new Exception(message)
                    }
                }
            }
        }
        try {
            parallel execs
        } finally {
            try {
                archiveArtifacts artifacts: "*.log"
            } catch (Exception e) {
                print('Exception while handling the log ' + e.toString())
            }
            sh 'rm -rf *'
            if (failed_threads > 0)
                throw new Exception(failed_threads + ' tests failed')
        }
    }
}