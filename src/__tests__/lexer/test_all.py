code = """
let IS_SOMETHING = true

function add(a, b) {
    let sum = a + b
    if (sum < 0) {
        return 0
    }
    return sum
}

if (IS_SOMETHING) {
    print("Something is true")
} else {
    print("Something is false")
}

radius = 3 * PI
height = add(2, 3)
let cylinder = Cylinder(radius=radius, height=height)

let v = cylinder.getVolume()

print(v)
"""
