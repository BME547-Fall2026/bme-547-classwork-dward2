from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

db = []


def add_to_database(n, i, letter, r, d):
    donor = {"name": n,
             "id": i,
             "blood_letter": letter,
             "rh_factor": r,
             "center": d}
    db.append(donor)


@app.route("/input", methods=["GET", "POST"])
def get_input():
    if request.method == "POST":
        donor_name = request.form["name_name"]
        donor_id = int(request.form["id_name"])
        blood_letter = request.form["letter_choice"]
        rh_factor = request.form.get("Rh_value")
        if rh_factor is None:
            rh_factor = "-"
        donation_center = request.form["center_name"]
        add_to_database(donor_name, donor_id, blood_letter, rh_factor,
                        donation_center)
        return redirect(url_for("get_menu"))

    return render_template("web_gui.html")


@app.route("/menu", methods=["GET", "POST"])
def get_menu():
    """
        Get the Form info
        If they want to add another, redirect to /input
        If they want the directory, redirect to /directory
    """
    if request.method == "POST":
        choice = request.form["choice"]
        if choice == "Another":
            return redirect(url_for("get_input"))
        else:
            return redirect(url_for("get_directory"))

    return render_template("menu.html")


@app.route("/directory", methods=["GET"])
def get_directory():
    return render_template("directory.html",
                           patients=db)


if __name__ == "__main__":
    app.run()
