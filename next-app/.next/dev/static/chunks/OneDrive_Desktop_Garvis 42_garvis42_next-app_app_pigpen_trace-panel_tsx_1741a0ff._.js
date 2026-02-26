(globalThis.TURBOPACK || (globalThis.TURBOPACK = [])).push([typeof document === "object" ? document.currentScript : undefined,
"[project]/OneDrive/Desktop/Garvis 42/garvis42/next-app/app/pigpen/trace-panel.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>TracePanel
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$OneDrive$2f$Desktop$2f$Garvis__42$2f$garvis42$2f$next$2d$app$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/OneDrive/Desktop/Garvis 42/garvis42/next-app/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$OneDrive$2f$Desktop$2f$Garvis__42$2f$garvis42$2f$next$2d$app$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/OneDrive/Desktop/Garvis 42/garvis42/next-app/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$OneDrive$2f$Desktop$2f$Garvis__42$2f$garvis42$2f$next$2d$app$2f$src$2f$components$2f$ui$2f$card$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/OneDrive/Desktop/Garvis 42/garvis42/next-app/src/components/ui/card.tsx [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
"use client";
;
;
function TracePanel() {
    _s();
    const [traces, setTraces] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$OneDrive$2f$Desktop$2f$Garvis__42$2f$garvis42$2f$next$2d$app$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])([]);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$OneDrive$2f$Desktop$2f$Garvis__42$2f$garvis42$2f$next$2d$app$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "TracePanel.useEffect": ()=>{
            fetch("/api/invocations/recent").then({
                "TracePanel.useEffect": (res)=>res.json()
            }["TracePanel.useEffect"]).then({
                "TracePanel.useEffect": (data)=>setTraces(data)
            }["TracePanel.useEffect"]);
        }
    }["TracePanel.useEffect"], []);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$OneDrive$2f$Desktop$2f$Garvis__42$2f$garvis42$2f$next$2d$app$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$OneDrive$2f$Desktop$2f$Garvis__42$2f$garvis42$2f$next$2d$app$2f$src$2f$components$2f$ui$2f$card$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Card"], {
        className: "bg-neutral-950 border border-neutral-800 mt-8",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$OneDrive$2f$Desktop$2f$Garvis__42$2f$garvis42$2f$next$2d$app$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$OneDrive$2f$Desktop$2f$Garvis__42$2f$garvis42$2f$next$2d$app$2f$src$2f$components$2f$ui$2f$card$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["CardHeader"], {
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$OneDrive$2f$Desktop$2f$Garvis__42$2f$garvis42$2f$next$2d$app$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$OneDrive$2f$Desktop$2f$Garvis__42$2f$garvis42$2f$next$2d$app$2f$src$2f$components$2f$ui$2f$card$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["CardTitle"], {
                    children: "Routing Trace Visualization"
                }, void 0, false, {
                    fileName: "[project]/OneDrive/Desktop/Garvis 42/garvis42/next-app/app/pigpen/trace-panel.tsx",
                    lineNumber: 17,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/OneDrive/Desktop/Garvis 42/garvis42/next-app/app/pigpen/trace-panel.tsx",
                lineNumber: 16,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$OneDrive$2f$Desktop$2f$Garvis__42$2f$garvis42$2f$next$2d$app$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$OneDrive$2f$Desktop$2f$Garvis__42$2f$garvis42$2f$next$2d$app$2f$src$2f$components$2f$ui$2f$card$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["CardContent"], {
                className: "flex flex-col gap-4",
                children: traces.length === 0 ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$OneDrive$2f$Desktop$2f$Garvis__42$2f$garvis42$2f$next$2d$app$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "text-neutral-400",
                    children: "No traces found."
                }, void 0, false, {
                    fileName: "[project]/OneDrive/Desktop/Garvis 42/garvis42/next-app/app/pigpen/trace-panel.tsx",
                    lineNumber: 21,
                    columnNumber: 11
                }, this) : traces.map((trace, idx)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$OneDrive$2f$Desktop$2f$Garvis__42$2f$garvis42$2f$next$2d$app$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "bg-neutral-900 rounded p-4 mb-2",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$OneDrive$2f$Desktop$2f$Garvis__42$2f$garvis42$2f$next$2d$app$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "text-orange-400 font-bold",
                                children: [
                                    "Domain: ",
                                    trace.domain
                                ]
                            }, void 0, true, {
                                fileName: "[project]/OneDrive/Desktop/Garvis 42/garvis42/next-app/app/pigpen/trace-panel.tsx",
                                lineNumber: 25,
                                columnNumber: 15
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$OneDrive$2f$Desktop$2f$Garvis__42$2f$garvis42$2f$next$2d$app$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "text-neutral-300",
                                children: [
                                    "Trigger: ",
                                    trace.trigger
                                ]
                            }, void 0, true, {
                                fileName: "[project]/OneDrive/Desktop/Garvis 42/garvis42/next-app/app/pigpen/trace-panel.tsx",
                                lineNumber: 26,
                                columnNumber: 15
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$OneDrive$2f$Desktop$2f$Garvis__42$2f$garvis42$2f$next$2d$app$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "text-neutral-300",
                                children: [
                                    "Provider: ",
                                    trace.provider
                                ]
                            }, void 0, true, {
                                fileName: "[project]/OneDrive/Desktop/Garvis 42/garvis42/next-app/app/pigpen/trace-panel.tsx",
                                lineNumber: 27,
                                columnNumber: 15
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$OneDrive$2f$Desktop$2f$Garvis__42$2f$garvis42$2f$next$2d$app$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "text-neutral-300",
                                children: "Operator Scores:"
                            }, void 0, false, {
                                fileName: "[project]/OneDrive/Desktop/Garvis 42/garvis42/next-app/app/pigpen/trace-panel.tsx",
                                lineNumber: 28,
                                columnNumber: 15
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$OneDrive$2f$Desktop$2f$Garvis__42$2f$garvis42$2f$next$2d$app$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("ul", {
                                className: "ml-4",
                                children: Object.entries(trace.operator_scores).map(([op, score])=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$OneDrive$2f$Desktop$2f$Garvis__42$2f$garvis42$2f$next$2d$app$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
                                        className: "text-neutral-200",
                                        children: [
                                            op,
                                            ": ",
                                            score
                                        ]
                                    }, op, true, {
                                        fileName: "[project]/OneDrive/Desktop/Garvis 42/garvis42/next-app/app/pigpen/trace-panel.tsx",
                                        lineNumber: 31,
                                        columnNumber: 19
                                    }, this))
                            }, void 0, false, {
                                fileName: "[project]/OneDrive/Desktop/Garvis 42/garvis42/next-app/app/pigpen/trace-panel.tsx",
                                lineNumber: 29,
                                columnNumber: 15
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$OneDrive$2f$Desktop$2f$Garvis__42$2f$garvis42$2f$next$2d$app$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "text-neutral-300",
                                children: "Timeline:"
                            }, void 0, false, {
                                fileName: "[project]/OneDrive/Desktop/Garvis 42/garvis42/next-app/app/pigpen/trace-panel.tsx",
                                lineNumber: 34,
                                columnNumber: 15
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$OneDrive$2f$Desktop$2f$Garvis__42$2f$garvis42$2f$next$2d$app$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("ul", {
                                className: "ml-4",
                                children: trace.timeline.map((event, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$OneDrive$2f$Desktop$2f$Garvis__42$2f$garvis42$2f$next$2d$app$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
                                        className: "text-neutral-400",
                                        children: [
                                            event.event,
                                            " @ ",
                                            event.timestamp
                                        ]
                                    }, i, true, {
                                        fileName: "[project]/OneDrive/Desktop/Garvis 42/garvis42/next-app/app/pigpen/trace-panel.tsx",
                                        lineNumber: 37,
                                        columnNumber: 19
                                    }, this))
                            }, void 0, false, {
                                fileName: "[project]/OneDrive/Desktop/Garvis 42/garvis42/next-app/app/pigpen/trace-panel.tsx",
                                lineNumber: 35,
                                columnNumber: 15
                            }, this)
                        ]
                    }, idx, true, {
                        fileName: "[project]/OneDrive/Desktop/Garvis 42/garvis42/next-app/app/pigpen/trace-panel.tsx",
                        lineNumber: 24,
                        columnNumber: 13
                    }, this))
            }, void 0, false, {
                fileName: "[project]/OneDrive/Desktop/Garvis 42/garvis42/next-app/app/pigpen/trace-panel.tsx",
                lineNumber: 19,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/OneDrive/Desktop/Garvis 42/garvis42/next-app/app/pigpen/trace-panel.tsx",
        lineNumber: 15,
        columnNumber: 5
    }, this);
}
_s(TracePanel, "TxvJui8ELIoPNMd+BQ3ueEXZZ1E=");
_c = TracePanel;
var _c;
__turbopack_context__.k.register(_c, "TracePanel");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/OneDrive/Desktop/Garvis 42/garvis42/next-app/app/pigpen/trace-panel.tsx [app-client] (ecmascript, next/dynamic entry)", ((__turbopack_context__) => {

__turbopack_context__.n(__turbopack_context__.i("[project]/OneDrive/Desktop/Garvis 42/garvis42/next-app/app/pigpen/trace-panel.tsx [app-client] (ecmascript)"));
}),
]);

//# sourceMappingURL=OneDrive_Desktop_Garvis%2042_garvis42_next-app_app_pigpen_trace-panel_tsx_1741a0ff._.js.map