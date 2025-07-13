export interface Survey {
    title: string
    internalName: string
    startDate: Date | null
    endDate: Date | null
    tags: string[]
    questions: any[]
}


export interface Question {
    label: string
    question: string
    type: 'text' | 'numberical' | 'custom'
    options?: CustomResponse[]
}

export interface QuestionType {
    value: string;
    label: string;
}

export interface CustomResponse {
    label: string
}