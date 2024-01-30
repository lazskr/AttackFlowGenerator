const getAnnotationsFromLocalStorage = () => {
    return JSON.parse(localStorage.getItem("annotations")) || [];
};

function setAnnotationsToLocalStorage(annotations) {
    try {
        localStorage.setItem("annotations", JSON.stringify(annotations));
    } catch (e) {
        console.error("Failed to save annotations to local storage:", e);
    }
}

export function addAnnotationToLocalStorage(annotation) {
    const annotations = getAnnotationsFromLocalStorage();

    const annotationData = {
        id: annotation.id,
        ranges: annotation.ranges,
        quote: annotation.quote,
        text: annotation.text,
        tags: annotation.tags || [],
    };

    const newAnnotations = [...annotations, annotationData];

    setAnnotationsToLocalStorage(newAnnotations);
}

export function updateAnnotationInLocalStorage(updatedAnnotation) {
    const annotations = getAnnotationsFromLocalStorage();

    let index = annotations.findIndex(
        (annot) => annot.id === updatedAnnotation.id,
    );

    // cannot store highlights property in local storage (cyclical reference)
    const updatedAnnotationToStore = { ...updatedAnnotation };
    delete updatedAnnotationToStore.highlights;

    annotations[index] = updatedAnnotationToStore;

    setAnnotationsToLocalStorage(annotations);
}

export function deleteAnnotationFromLocalStorage(annotation) {
    const annotations = getAnnotationsFromLocalStorage();

    let newAnnotations = annotations.filter(
        (annot) => annot.id !== annotation.id,
    );

    setAnnotationsToLocalStorage(newAnnotations);
}
