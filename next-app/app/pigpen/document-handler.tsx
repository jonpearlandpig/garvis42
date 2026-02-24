"use client";
import { useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

export default function DocumentHandler() {
  const fileInput = useRef<HTMLInputElement>(null);
  const [fileType, setFileType] = useState<string>("pdf");
  const [action, setAction] = useState<string>("create");
  const [content, setContent] = useState<string>("");
  const [outputUrl, setOutputUrl] = useState<string>("");

  // Simple PDF creation (client-side, no backend)
  function handleCreate() {
    if (fileType === "pdf") {
      const blob = new Blob([
        `%PDF-1.3\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 144] /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 44 >>\nstream\nBT /F1 24 Tf 100 100 Td (${content || "Test PDF"}) Tj ET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000010 00000 n \n0000000060 00000 n \n0000000117 00000 n \n0000000216 00000 n \ntrailer\n<< /Root 1 0 R /Size 5 >>\nstartxref\n316\n%%EOF`
      ], { type: "application/pdf" });
      setOutputUrl(URL.createObjectURL(blob));
    } else if (fileType === "docx") {
      const blob = new Blob([
        `PK\u0003\u0004...docx placeholder...${content}`
      ], { type: "application/vnd.openxmlformats-officedocument.wordprocessingml.document" });
      setOutputUrl(URL.createObjectURL(blob));
    } else if (fileType === "xlsx") {
      const blob = new Blob([
        `PK\u0003\u0004...xlsx placeholder...${content}`
      ], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
      setOutputUrl(URL.createObjectURL(blob));
    }
  }

  return (
    <Card className="bg-neutral-950 border border-neutral-800 mt-8">
      <CardHeader>
        <CardTitle>Document Handler (No Backend)</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <div className="flex gap-2">
          <select className="bg-neutral-900 text-white border-neutral-700 rounded px-2 py-1" value={fileType} onChange={e => setFileType(e.target.value)}>
            <option value="pdf">PDF</option>
            <option value="docx">DOCX</option>
            <option value="xlsx">XLSX</option>
          </select>
          <select className="bg-neutral-900 text-white border-neutral-700 rounded px-2 py-1" value={action} onChange={e => setAction(e.target.value)}>
            <option value="create">Create</option>
            {/* <option value="read">Read</option>
            <option value="edit">Edit</option> */}
          </select>
        </div>
        <Input className="bg-neutral-900 border-neutral-700 text-white" placeholder="Document content..." value={content} onChange={e => setContent(e.target.value)} />
        <Button className="bg-orange-500 text-black" onClick={handleCreate}>Create Document</Button>
        {outputUrl && (
          <a href={outputUrl} download={`output.${fileType}`} className="text-orange-400 underline mt-2">Download {fileType.toUpperCase()}</a>
        )}
      </CardContent>
    </Card>
  );
}
