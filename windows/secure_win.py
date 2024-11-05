import subprocess

process = subprocess.Popen(["net", "share"])
process.wait()