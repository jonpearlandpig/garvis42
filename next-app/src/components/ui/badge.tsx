import * as React from "react";

export function Badge({ className = "", ...props }: React.HTMLAttributes<HTMLSpanElement>) {
  return <span className={`inline-block rounded px-2 py-1 text-xs font-bold ${className}`} {...props} />;
}
