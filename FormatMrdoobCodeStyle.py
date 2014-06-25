import sublime
import sublime_plugin
import glob
import os, sys, platform, subprocess, webbrowser, json, re, time, atexit

windows = platform.system() == "Windows"
python3 = sys.version_info[0] > 2
is_st2 = int(sublime.version()) < 3000
plugin_dir = os.path.abspath(os.path.dirname(__file__))
threejs_dir = ''

class FormatMrdoobCodeStyleCommand(sublime_plugin.WindowCommand):
    def executeCommand(self, command,cwd = plugin_dir):
        print(" ".join(command))
        print(cwd)
        proc = ''
        if hasattr(subprocess, "check_output"):
            subprocess.check_output(command, cwd=cwd, shell=windows)
        else:
            subprocess.check_call(command, cwd=cwd, shell=windows)

    def installComponents(self):
        nessecary_commands = True
        try:
            self.executeCommand(["codepainter", "-h"])
            self.executeCommand(["jscs","-h"])
        except:
            nessecary_commands = False
        if not nessecary_commands:
            if sublime.ok_cancel_dialog(
                "It appears Tern has not been installed. Do you want tern_for_sublime to try and install it? "
                "(Note that this will only work if you already have node.js and npm installed on your system.)"
                "\n\nTo get rid of this dialog, either uninstall tern_for_sublime, or set the tern_command setting.",
                "Yes, install."):
                try:
                    self.executeCommand(["npm", "install", "-g", "jscs"])
                except subprocess.CalledProcessError as e:
                    msg = "Installation failed. Try doing 'npm install -g jscs' manually in " + plugin_dir + "."
                    if hasattr(e, "output"):
                        msg += " Error message was:\n\n" + e.output
                    sublime.error_message(msg)
                    return False
                try:
                    self.executeCommand(["npm", "install", "-g", "codepainter"])
                except:
                    msg = "Installation failed. Try doing 'npm install -g codepainter' manually in " + plugin_dir + "."
                    if hasattr(e, "output"):
                        msg += " Error message was:\n\n" + e.output
                    sublime.error_message(msg)
                    return False
        return True
    def run(self):
        settings = sublime.load_settings("Preferences.sublime-settings")
        threejs_dir = settings.get("threejsdir", False)
        if self.installComponents():
            self.executeCommand(["codepainter", "xform", "-j",  os.path.join(plugin_dir, "mrdoob_codepainter.json"), "**/*.js"], os.path.join(threejs_dir,"src"))
            os.chdir(os.path.join(threejs_dir,"src"))
            for file in glob.glob("*.js"):
                with open(file,'rt') as f:
                    newlines = []
                    for line in f.readlines():
                        newlines.append(line.replace('( )', '()').replace('[ ]', '[]').replace('{ }', '{}'))
                with open(file, 'wt') as f:
                    for line in newlines:
                        f.write(line)
            try:
                self.executeCommand(["jscs", os.path.join(threejs_dir,"src"), "-c", "mrdoob.json", "-r", "spaces.js"], plugin_dir)
            except subprocess.CalledProcessError as e:
                if hasattr(e, "output"):
                    msg = " Error message was:\n\n" + e.output
                #sublime.error_message("test")

        else:
            print("ended wrong")


