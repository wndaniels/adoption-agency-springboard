from crypt import methods
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_adoption_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'yupp1234'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    """ Redirects user to "/pets" """
    return redirect('/pets')


@app.route('/pets')
def pets():
    """ Show list of all pets within the database. """
    pets = Pet.query.all()
    return render_template('/home/home_page.html', pets=pets)


@app.route('/pets/new', methods=["GET", "POST"])
def add_pet():
    """Render and handle form submission for adding a new pet."""
    form = AddPetForm()

    # handle validation of form on submit, if data does not meet the validation, render_tamplate on the add pet form, if validation is successful, add pet and redirect to "/pets".
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data or None
        age = form.age.data
        notes = form.notes.data

        pet = Pet(name=name, species=species, photo_url=photo_url,
                  age=age, notes=notes)

        db.session.add(pet)
        db.session.commit()
        return redirect('/pets')
    else:
        return render_template('/form/add_pet.html', form=form)


@app.route('/pets/<int:id>/details', methods=["GET", "POST"])
def pet_details(id):
    """Show details of select pet, and show / handle form to update pet information. """
    pet = Pet.query.get_or_404(id)
    form = EditPetForm(obj=pet)

    # handle validation of form on submit, if data does not meet the validation, render_tamplate on the details page, if validation is successful, update pet info.
    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()
        return redirect(f'/pets/{pet.id}/details')
    else:
        return render_template('/details/pet_details.html', pet=pet, form=form)
