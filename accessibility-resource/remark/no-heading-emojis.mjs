import {visit} from 'unist-util-visit'

// Similar regex to build plugin
const emojiRegex = /[\u{1F600}-\u{1F64F}]|[\u{1F300}-\u{1F5FF}]|[\u{1F680}-\u{1F6FF}]|[\u{1F700}-\u{1F77F}]|[\u{1F780}-\u{1F7FF}]|[\u{1F800}-\u{1F8FF}]|[\u{1F900}-\u{1F9FF}]|[\u{1FA00}-\u{1FAFF}]|[\u{2600}-\u{26FF}]|[\u{2700}-\u{27BF}]|[\u{FE00}-\u{FE0F}]|[\u{1F1E6}-\u{1F1FF}]|[\u{200D}]/gu

export default function noHeadingEmojis() {
  return (tree, file) => {
    visit(tree, 'heading', (node) => {
      let containsEmoji = false
      visit(node, 'text', (t) => {
        if (typeof t.value === 'string' && emojiRegex.test(t.value)) {
          containsEmoji = true
        }
      })
      if (containsEmoji) {
        file.message('Do not use emojis in headings (H1–H6). Use plain text and move decorative emojis outside headings).', node, 'no-heading-emojis')
      }
    })
  }
}
