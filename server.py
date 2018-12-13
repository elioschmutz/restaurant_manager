from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database_setup import Base, Restaurant, MenuItem, session

app = Flask(__name__)


@app.route('/')
@app.route('/restaurants/')
def listRestaurants():
    return render_template(
        'listRestaurants.html',
        restaurants=session.query(Restaurant).all())


@app.route('/restaurants/JSON')
def listRestaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify([restaurant.serialize for restaurant in restaurants])


@app.route('/restaurants/new', methods=['GET', 'POST'])
def addRestaurant():
    if request.method == 'POST':
        restaurant = Restaurant(name=request.form.get('name', ''))
        session.add(restaurant)
        session.commit()
        flash("Restaurant added")
        return redirect(url_for('listMenuItems', restaurant_id=restaurant.id))
    return render_template('addRestaurant.html')


@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        restaurant.name = request.form.get('name', '')
        session.add(restaurant)
        session.commit()
        flash("Restaurant edited")
        return redirect(url_for('listRestaurants'))
    return render_template('editRestaurant.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash("Restaurant deleted")
        return redirect(url_for('listRestaurants'))
    return render_template('deleteRestaurant.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def listMenuItems(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return render_template('listMenuItems.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/JSON')
def listMenuItemsJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return jsonify([menuitem.serialize for menuitem in restaurant.menuitems])


@app.route('/restaurants/<int:restaurant_id>/menu/add', methods=['GET', 'POST'])
def addMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        menuitem = MenuItem(
            name=request.form.get('name', ''),
            description=request.form.get('description', ''),
            price=request.form.get('price', ''),
            course=request.form.get('course', ''),
            restaurant_id=restaurant_id,
            )
        session.add(menuitem)
        session.commit()
        flash("Menu-Item added")
        return redirect(url_for('listMenuItems', restaurant_id=restaurant.id))
    return render_template('addMenuItem.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    menuitem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(menuitem)
        session.commit()
        flash("Menu-Item deleted")
        return redirect(url_for('listMenuItems', restaurant_id=restaurant_id))
    return render_template('deleteMenuItem.html', menuitem=menuitem)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    menuitem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        menuitem.name = request.form.get('name', '')
        menuitem.description = request.form.get('description', '')
        menuitem.price = request.form.get('price', '')
        menuitem.course = request.form.get('course', '')
        menuitem.restaurant_id = restaurant_id
        print request.form.get('name')
        session.add(menuitem)

        session.commit()
        flash("Menu-Item edited")
        return redirect(url_for('listMenuItems', restaurant_id=restaurant_id))
    return render_template('editMenuItem.html', menuitem=menuitem)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    menuitem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(menuitem.serialize)


if __name__ == '__main__':
    app.secret_key = "super_secret"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
