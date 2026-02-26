import * as React from "react";

export function Accordion({ children, className = "", ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={`divide-y divide-neutral-800 ${className}`} {...props}>{children}</div>;
}
export function AccordionItem({ children, className = "", ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={`py-2 ${className}`} {...props}>{children}</div>;
}
export function AccordionTrigger({ children, className = "", ...props }: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return <button className={`w-full text-left font-bold py-2 px-2 bg-neutral-900 hover:bg-neutral-800 rounded ${className}`} {...props}>{children}</button>;
}
export function AccordionContent({ children, className = "", ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={`px-2 py-2 ${className}`} {...props}>{children}</div>;
}
