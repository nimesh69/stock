export function LoadingLine({ label = "Loading..." }: { label?: string }) {
  return <p className="muted">{label}</p>;
}

export function ErrorLine({ label }: { label: string }) {
  return <p className="auth-error">{label}</p>;
}
