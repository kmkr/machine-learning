const data = [];

function setup() {
    createCanvas(400, 400);
}

function linearRegression() {
    const {x:xsum, y:ysum} = data.reduce((prevVal, curVal) => {
        prevVal.x += curVal.x;
        prevVal.y += curVal.y;
        return prevVal;
    }, { x: 0, y: 0 });

    const xmean = xsum / data.length;
    const ymean = ysum / data.length;

    let numerator = 0;
    let denominator = 0;

    data.forEach(({x, y}) => {
        numerator += (x - xmean) * (y - ymean);
        denominator += (x - xmean) * (x - xmean);
    });

    const m = numerator / denominator;
    const b = ymean - m * xmean;

    return { b, m };
}

function drawLine(b, m) {
    const x1 = 0;
    const y1 = m * x1 + b;
    const x2 = 1;
    const y2 = m * x2 + b;
    stroke(255, 0, 255);

    const mx1 = map(x1, 0, 1, 0, width);
    const my1 = map(y1, 0, 1, height, 0);
    const mx2 = map(x2, 0, 1, 0, width);
    const my2 = map(y2, 0, 1, height, 0);
    line(mx1, my1, mx2, my2);
}

function mousePressed() {
    const x = map(mouseX, 0, width, 0, 1);
    const y = map(mouseY, 0, height, 1, 0);
    
    const point = createVector(x, y);
    data.push(point)
}

function draw() {
    background(51);    
    data.forEach(elem => {
        const x = map(elem.x, 0, 1, 0, width);
        const y = map(elem.y, 0, 1, height, 0);
        fill(255);
        stroke(255);
        ellipse(x, y, 8, 8);
    });

    if (data.length > 1) {
        const { b, m } = linearRegression();
        drawLine(b, m);
    }
}
