from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            "title",
            "excerpt",
            "content",
            "cover_image",
            "category",
            "tags",
            "is_published",
        )
        widgets = {
            "tags": forms.CheckboxSelectMultiple(),
            "excerpt": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "cover_image": forms.FileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tags"].required = False
        self.fields["is_published"].widget.attrs.setdefault("class", "form-check-input")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(
                attrs={"rows": 3, "class": "form-control", "placeholder": "Write a comment…"}
            ),
        }
