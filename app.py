
# Media upload
@app.route('/admin/media/upload', methods=['GET','POST'])
@login_required
def media_upload():
form = MediaForm()
if form.validate_on_submit() and form.file.data:
filename = save_file(form.file.data)
media_type = 'video' if filename.lower().endswith(('mp4','webm')) else 'image'
m = Media(filename=filename, caption=form.caption.data, media_type=media_type)
db.session.add(m)
db.session.commit()
flash('Media uploaded.', 'success')
return redirect(url_for('admin_dashboard'))
return render_template('admin/media_upload.html', form=form)


# Basic purchase placeholder
@app.route('/buy/<int:product_id>', methods=['GET','POST'])
def buy_product(product_id):
product = Product.query.get_or_404(product_id)
flash('To purchase, follow the payment link (not implemented).', 'info')
return redirect(url_for('product_detail', product_id=product_id))


# Admin setup route - create initial admin (remove or protect in production)
@app.route('/admin/setup')
def admin_setup():
if Admin.query.first():
return 'Admin exists'
user = Admin(username='admin', password_hash=generate_password_hash('changeme'))
db.session.add(user)
db.session.commit()
return 'Admin created (username=admin, password=changeme)'


return app


if __name__ == '__main__':
app = create_app()
app.run(debug=True)
