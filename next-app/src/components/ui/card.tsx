import * as React from "react";

export function Card({ className = "", ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={`rounded-xl shadow-sm ${className}`} {...props} />;
}
export function CardHeader({ className = "", ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={`px-6 pt-6 pb-2 ${className}`} {...props} />;
}
export function CardTitle({ className = "", ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <h3 className={`font-bold text-lg ${className}`} {...props} />;
}
export function CardContent({ className = "", ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={`px-6 pb-6 ${className}`} {...props} />;
}
