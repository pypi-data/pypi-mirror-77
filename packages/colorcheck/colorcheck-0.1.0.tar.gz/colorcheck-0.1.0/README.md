# Colorcheck

Colorcheck is a color contrast checker.

It indicates, in a CSS file, the contrast between background and foreground
colors for each CSS rule (for the 0.1 version, when the rule includes color and
background-color attributes).

A simple example
----------------

Let's consider the following CSS code (in a file named "simple.css") :

`body {
	background-color: lightblue;
	color: red;
}`

The command :

`$ python3 colorcheck.py simple.css`

will return :

`body : 2.62`
