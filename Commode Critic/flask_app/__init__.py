from flask import Flask, render_template, redirect ,session ,request , flash, jsonify

app = Flask(__name__)    
app.secret_key="spooky"
