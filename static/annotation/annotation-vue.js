const { createApp, ref, reactive, watch, computed } = Vue;

const objectTypes = ["attackAction", "attackAsset"];

const attackActionSchema = [
    { id: "technique_id", label: "Technique ID", type: "text" },
    { id: "action_name", label: "Name", type: "text" },
    { id: "technique_ref", label: "Technique Reference", type: "text" },
    { id: "action_description", label: "Description", type: "textarea" },
    {
        id: "asset_refs",
        label: "Asset References (comma separated)",
        type: "text",
    },
    {
        id: "effect_refs",
        label: "Effect References (comma separated)",
        type: "text",
    },
];

const attackAssetSchema = [
    { id: "asset_name", label: "Name", type: "text" },
    { id: "asset_description", label: "Description", type: "textarea" },
    { id: "object_ref", label: "Object Reference", type: "text" },
];

createApp({
    delimiters: ["[[", "]]"],
    // emit
    setup() {
        // state for annotations

        //const message = ref('Hello vue!')
        const reportName = window.reportName;
        const annotations = ref(window.annotation.annotations);
        const isSaving = ref(false);
        // const tempAnnotation = reactive({
        //     id: '',
        //     technique_id: '',
        //     action_name: '',
        //     technique_ref: '',
        //     action_description: '',
        //     asset_refs: '',
        //     effect_refs: ''
        // });
        const tempAnnotation = reactive({});

        const selectedAnnotationId = ref("");

        const selectedType = ref("");

        const currentSchema = computed(() => {
            switch (selectedType.value) {
                case "attackAction":
                    return attackActionSchema;
                case "attackAsset":
                    return attackAssetSchema;
                default:
                    return [];
            }
        });

        watch(selectedAnnotationId, (newId) => {
            checkNDeleteTempAnnotation();
            const matchingAnnotation = annotations.value.find(
                (a) => a.id === newId,
            );
            if (matchingAnnotation) {
                Object.assign(tempAnnotation, matchingAnnotation);
                selectedType.value = matchingAnnotation.type;
            }
        });

        watch(selectedType, (newType) => {
            if (JSON.stringify(tempAnnotation) !== "{}") {
                if (tempAnnotation.id.length > 0) {
                    const existingIndex = annotations.value.findIndex(
                        (a) => a.id === tempAnnotation.id,
                    );
                    if (existingIndex === -1) {
                        for (const key in tempAnnotation) {
                            // Skip the 'id' key and delete all others
                            if (key !== "id") {
                                delete tempAnnotation[key];
                            }
                        }

                        // Based on the selected type, get the new schema
                        let newSchema = [];
                        switch (newType) {
                            case "attackAction":
                                newSchema = attackActionSchema;
                                break;
                            case "attackAsset":
                                newSchema = attackAssetSchema;
                                break;
                        }

                        // Assign default values (empty) for the new schema
                        newSchema.forEach((field) => {
                            tempAnnotation[field.id] = ""; // Assuming default empty value for all fields.
                        });
                        console.log(tempAnnotation);
                    }
                }
            }
        });

        document.addEventListener("annotationCreated", (e) => {
            checkNDeleteTempAnnotation();
            if (selectedAnnotationId !== "") {
                selectedAnnotationId.value = "";

                for (const key in tempAnnotation) {
                    tempAnnotation[key] = "";
                }
            }

            tempAnnotation.id = e.detail.id;
        });

        //check to see if temp annotation exists but not saved & del
        function checkNDeleteTempAnnotation() {
            if (JSON.stringify(tempAnnotation) !== "{}") {
                if (tempAnnotation.id.length > 0) {
                    const existingIndex = annotations.value.findIndex(
                        (a) => a.id === tempAnnotation.id,
                    );

                    if (existingIndex === -1) {
                        cancelAnnotation();
                    }
                }
            }
        }

        document.addEventListener("annotationSelected", (e) => {
            checkNDeleteTempAnnotation();

            // look through annotations array
            const selectedId = e.detail.id;
            const matchingAnnotation = annotations.value.find(
                (a) => a.id === selectedId,
            );

            // temp annotation = the matching annotation
            if (matchingAnnotation) {
                Object.assign(tempAnnotation, matchingAnnotation);
                selectedAnnotationId.value = selectedId;
            }
        });

        function handleSubmit() {
            console.log(tempAnnotation);

            const existingIndex = annotations.value.findIndex(
                (a) => a.id === tempAnnotation.id,
            );

            if (existingIndex !== -1) {
                annotations.value[existingIndex] = { ...tempAnnotation };
            } else {
                annotations.value.push({
                    ...tempAnnotation,
                    type: selectedType.value,
                });
            }

            // Reset tempAnnotation
            for (const key in tempAnnotation) {
                delete tempAnnotation[key];
            }

            selectedAnnotationId.value = "";
            selectedType.value = "";
        }

        function cancelAnnotation() {
            const existingIndex = annotations.value.findIndex(
                (a) => a.id === tempAnnotation.id,
            );

            if (existingIndex === -1) {
                const id = tempAnnotation.id;

                for (const key in tempAnnotation) {
                    delete tempAnnotation[key];
                }

                const event = new CustomEvent("annotationCancelled", {
                    detail: { id: id },
                });
                document.dispatchEvent(event);
            }

            selectedAnnotationId.value = "";
            selectedType.value = "";
        }

        async function saveAnnotations() {
            isSaving.value = true;
            const csrftoken = window.getCookie("csrftoken");
            let res = await fetch(window.location.href, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken,
                },
                body: JSON.stringify({
                    highlights: window.highlights,
                    annotations: annotations.value,
                }),
            });
            if (res.ok) {
                window.location.replace(`/reports/${window.reportId}`);
            }
            isSaving.value = false;
        }

        async function approveAnnotations() {
            isSaving.value = true;
            const csrftoken = window.getCookie("csrftoken");
            let res = await fetch(window.location.href, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken,
                },
            });
            if (res.ok) {
                window.location.replace(`/reports/${window.reportId}`);
            }
            isSaving.value = false;
        }

        return {
            annotations,
            isSaving,
            reportName,
            tempAnnotation,
            selectedAnnotationId,
            objectTypes,
            currentSchema,
            selectedType,
            handleSubmit,
            cancelAnnotation,
            saveAnnotations,
            approveAnnotations,
        };
    },
}).mount("#app");
