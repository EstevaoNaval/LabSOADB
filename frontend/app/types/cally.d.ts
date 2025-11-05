// types/cally.d.ts
declare module 'cally' {
  export {}
}

declare global {
    namespace JSX {
        interface IntrinsicElements {
            'calendar-date': any
            'calendar-month': any
            'calendar-range': any
        }
    }
}
