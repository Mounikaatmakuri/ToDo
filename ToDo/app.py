from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

items = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/items')
def view_items():
    return render_template('items.html', items=items)

@app.route('/items/new', methods=['GET', 'POST'])
def create_item():
    if request.method == 'POST':
        task = request.form['task']
        description = request.form.get('description', '')
        new_id = max((item['id'] for item in items), default=0) + 1
        items.append({"id": new_id, "Task": task, "description": description})
        return redirect(url_for('view_items'))
    return render_template('new_item.html')

@app.route('/items/<int:item_id>/edit', methods=['GET', 'POST'])
def edit_item(item_id):
    item = next((i for i in items if i['id'] == item_id), None)
    if not item:
        return "Item not found", 404

    if request.method == 'POST':
        item['Task'] = request.form['task']
        item['description'] = request.form.get('description', '')
        return redirect(url_for('view_items'))

    return render_template('edit_item.html', item=item)

@app.route('/items/<int:item_id>/delete', methods=['POST'])
def delete_item(item_id):
    global items
    items = [i for i in items if i['id'] != item_id]
    return redirect(url_for('view_items'))

if __name__ == '__main__':
    app.run(debug=True)