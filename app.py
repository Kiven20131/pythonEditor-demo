from flask import Flask,render_template,request
import sys,os,subprocess,tempfile
#inport necessary libraries
#tempfile to create a temporary file whereby we execute the code and return the output along with any error messages
#os to ensure we can delete the alloted temp file
#subprocess so that we can execute a python interpreter
#sys is essential in order to ensure that the correct command is usedimport subprocess,tempfile , os,sys
app = Flask(__name__)
def runCode(code:str ,user_input: str = "" ,timeout: int = 30) -> str:
    #code could encounter error messages
        try:
            fd, temp_path = tempfile.mkstemp(suffix=".py")
            #creating a path whereby we can delete the file and use it
            with os.fdopen(fd, "w") as f:
                f.write(code)
            #utilise subprocess and put the return value into a variable
            #python interpreter
            #stdin
            result = subprocess.run(
                [sys.executable,temp_path],
                capture_output=True,
                input=user_input,
                text=True,
                #if it takes more than 30 seconds quit because that means something is probably utilising too many resources
                timeout=timeout
            )
            #put the actual result into output whether it be error messages or it be successful
            return result.stdout + result.stderr
        #make sure that it doesn't take too long
        except subprocess.TimeoutExpired:
          return "Execution timed out!"
        #should any errors occur
        #the output should be the error message
        except Exception as e:
            return f"Error: {e}"
        finally:
            if 'temp_path' in locals() and os.path.exists(temp_path):
              os.remove(temp_path)
# define a function by the route /
@app.route("/",methods=["POST","GET"])
def index():
    output = ""
    code = ""
    user_input=""
    if request.method == "POST":
        code = request.form.get("code","")
        user_input = request.form.get("user_input","")
        if not code.strip():
            output = "No code has been provided."
            return render_template("pythonEditor.html" , output = output ,code=code,user_input=user_input)
        else:
            output = runCode(code,user_input)
    return render_template("pythonEditor.html",output=output, code=code,user_input = user_input)
