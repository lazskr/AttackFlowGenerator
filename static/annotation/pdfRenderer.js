import { v4 as uuidv4 } from "https://jspm.dev/uuid";

pdfjsLib.GlobalWorkerOptions.workerSrc =
    "https://unpkg.com/pdfjs-dist@3.10.111/build/pdf.worker.min.js";

let pdfContainer;
let properties;
let target = null;
let canvas;
let textLayer;

let pdf = null;
let scale = 1.5;
let pageRendering = false;
let pageNumPending = null;
let pageNum = 1;
let highlights = window.annotation.highlights;
window.highlights = highlights;
let selectedId = null;

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
}
window.getCookie = getCookie;

function pick(node) {
    if (!node) {
        if (target) target.classList.remove("target");
        target = null;
        return;
    }

    let inputBox = node.parentElement.querySelector("input");
    if (target == inputBox) {
        inputBox.classList.remove("target");
        target = null;
        return;
    }

    if (target) target.classList.remove("target");
    target = inputBox;
    inputBox.classList.add("target");
}

window.pick = pick;

function nextPage() {
    if (pageNum >= pdf.numPages) return;
    pageNum += 1;
    queueRenderPage(pageNum);
}

window.nextPage = nextPage;

function prevPage() {
    if (pageNum <= 1) return;
    pageNum -= 1;
    queueRenderPage(pageNum);
}

window.prevPage = prevPage;

function zoomIn() {
    if (scale >= 4) return;
    scale += 0.25;
    queueRenderPage(pageNum);
}

window.zoomIn = zoomIn;

function zoomOut() {
    if (scale <= 0.25) return;
    scale -= 0.25;
    queueRenderPage(pageNum);
}

window.zoomOut = zoomOut;

document.addEventListener("annotationCancelled", (e) => {
    const pageIndex = highlights[pageNum].findIndex(
        (h) => h.id === e.detail.id,
    );

    if (pageIndex !== -1) {
        highlights[pageNum].splice(pageIndex, 1);
    }

    queueRenderPage(pageNum);
});

function queueRenderPage(num) {
    if (pageRendering) {
        pageNumPending = num;
    } else {
        renderPage(num);
    }
}

async function renderPage(num) {
    pageRendering = true;
    let page = await pdf.getPage(num);
    const viewport = page.getViewport({ scale: scale });

    // Prepare canvas using PDF page dimensions
    let newCanvas = document.createElement("canvas");
    let context = newCanvas.getContext("2d");
    newCanvas.height = viewport.height;
    newCanvas.width = viewport.width;

    // Render PDF page into canvas context
    let renderContext = {
        canvasContext: context,
        viewport: viewport,
    };
    let renderTask = page.render(renderContext);
    await renderTask.promise;

    pageRendering = false;
    textLayer.textContent = "";
    canvas.replaceWith(newCanvas);
    canvas = newCanvas;
    pdfContainer.style.setProperty("--scale-factor", scale);

    if (pageNumPending !== null) {
        let num = pageNumPending;
        pageNumPending = null;
        await renderPage(num);
        return;
    }

    let textContent = await page.getTextContent();
    let newTextLayer = document.createElement("div");
    newTextLayer.classList.add("textLayer");
    newTextLayer.style.margin = "0 auto";
    pdfjsLib.renderTextLayer({
        textContentSource: textContent,
        container: newTextLayer,
        viewport: viewport,
    });

    let pageHighlights = highlights[num];
    if (pageHighlights) {
        for (let hl of pageHighlights) {
            for (let rect of hl.coords) {
                let bounds = viewport.convertToViewportRectangle(rect);

                var x1 = Math.min(bounds[0], bounds[2]);
                var y1 = Math.min(bounds[1], bounds[3]);
                var width = Math.abs(bounds[0] - bounds[2]);
                var hight = Math.abs(bounds[1] - bounds[3]);

                var el = createRectDiv([x1, y1, width, hight], hl.hue, hl.id);
                newTextLayer.appendChild(el);
            }
        }
    }
    textLayer.replaceWith(newTextLayer);
    textLayer = newTextLayer;
    textLayer.onmouseup = () => {
        let text = window.getSelection().toString().replaceAll("\n", " ");
        if (text.length > 0 && target != null) {
            target.value = text;
            pick(null);
            showHighlight(text);
        }
    };
}

async function showHighlight(text) {
    let page = await pdf.getPage(pageNum);
    let pageRect = canvas.getClientRects()[0];
    let selectionRects = window.getSelection().getRangeAt(0).getClientRects();
    let viewport = page.getViewport({ scale: scale });
    let selectionRectsList = Object.values(selectionRects);

    let coords = selectionRectsList.map((r) => {
        return viewport
            .convertToPdfPoint(r.left - pageRect.x, r.top - pageRect.y)
            .concat(
                viewport.convertToPdfPoint(
                    r.right - pageRect.x,
                    r.bottom - pageRect.y,
                ),
            );
    });

    const hue = Math.floor(Math.random() * 360);
    const id = uuidv4();

    if (!highlights[pageNum]) {
        highlights[pageNum] = [];
    }

    highlights[pageNum].push({
        id: id,
        coords: coords,
        hue: hue,
        content: text,
    });

    for (let rect of coords) {
        let bounds = viewport.convertToViewportRectangle(rect);

        var x1 = Math.min(bounds[0], bounds[2]);
        var y1 = Math.min(bounds[1], bounds[3]);
        var width = Math.abs(bounds[0] - bounds[2]);
        var hight = Math.abs(bounds[1] - bounds[3]);

        var el = createRectDiv([x1, y1, width, hight], hue, id);
        textLayer.appendChild(el);
    }

    const event = new CustomEvent("annotationCreated", {
        detail: {
            id: id,
        },
    });
    document.dispatchEvent(event);
    window.getSelection().empty();
}

function createRectDiv(boundBox, hue, id) {
    var el = document.createElement("div");
    el.setAttribute("class", `hiDiv ${id}`);
    el.setAttribute(
        "style",
        `
            position: absolute;
            background-color: hsl(${hue}, 100%, 50%);
            opacity: 0.5;
            z-index: 1;
            cursor: pointer;
            left: ${boundBox[0]}px;
            top: ${boundBox[1]}px;
            width: ${boundBox[2]}px;
            height: ${boundBox[3]}px;
        `,
    );

    el.addEventListener("mouseover", () => {
        for (let hi of document.getElementsByClassName(id)) {
            hi.style.opacity = "1.0";
            hi.style.border = "1px solid black";
        }
    });

    el.addEventListener("mouseout", () => {
        for (let hi of document.getElementsByClassName(id)) {
            hi.style.opacity = "0.5";
            hi.style.border = "none";
        }
    });

    el.addEventListener("click", () => {
        const event = new CustomEvent("annotationSelected", {
            detail: { id: id },
        });
        document.dispatchEvent(event);
    });

    return el;
}

pdfContainer = document.getElementById("pdf-container");
properties = document.getElementById("properties");
canvas = document.createElement("canvas");
textLayer = document.createElement("div");
pdfContainer.appendChild(canvas);
pdfContainer.appendChild(textLayer);
pdfjsLib.getDocument(window.pdfUrl).promise.then(
    (p) => {
        console.log("PDF loaded");

        // Fetch the first page
        pdf = p;
        renderPage(1);
    },
    (err) => {
        // PDF loading error
        console.error(err);
    },
);
