---
title: Angular 基础教程-76
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>表单校验一定会牵扯到一个大家都比较头疼的技术点，那就是正则表达式，正则表达式学起来有难度，但是又不可或缺。</p>
<p>强制所有开发者都能精通正则表达式是不太现实的事情，但是有一点是必须要做到的，那就是至少要能读懂别人编写的正则。</p>
<h3 id="">先来一个例子</h3>
<p><img width="50%" src="https://images.gitbook.cn/bd380a10-f380-11e8-af6e-271f68300704"></p>
<p>关键 HTML 模板代码如下：</p>
<pre>
    &lt;form #registerForm="ngForm" class="form-horizontal"&gt;
      &lt;div class="form-group" [ngClass]="{'has-error': userName.invalid && (userName.dirty || userName.touched) }"&gt;
        &lt;label class="col-xs-2 control-label"&gt;用户名：&lt;/label&gt;
        &lt;div class="col-xs-10"&gt;
          &lt;input #userName="ngModel" [(ngModel)]="regModel.userName" name="userName" type="email" class="form-control" placeholder="Email" required minlength="12" maxlength="32"&gt;
          &lt;div *ngIf="userName.invalid && (userName.dirty || userName.touched)" class="text-danger"&gt;
            &lt;div *ngIf="userName.errors.required"&gt;
              用户名不能为空
            &lt;/div&gt;
            &lt;div *ngIf="userName.errors.minlength"&gt;
              最小长度不能小于12个字符
            &lt;/div&gt;
            &lt;div *ngIf="userName.errors.maxlength"&gt;
              最大长度不能大于32个字符
            &lt;/div&gt;
          &lt;/div&gt;
        &lt;/div&gt;
      &lt;/div&gt;
    &lt;/form&gt;

    &lt;div class="panel-footer"&gt;
        &lt;p&gt;用户名：{{userName.value}}&lt;/p&gt;
        &lt;p&gt;密码：{{pwd.value}}&lt;/p&gt;
        &lt;p&gt;表单状态： {{registerForm.valid}} 
                    {{registerForm.invalid}} 
                    {{registerForm.pending}} 
                    {{registerForm.pristine}} 
                    {{registerForm.dirty}}
                    {{registerForm.untouched}} 
                    {{registerForm.touched}}
        &lt;/p&gt;
    &lt;/div&gt;
</pre>
<p>模板和组件里面的关键代码：</p>
<pre><code>export class RegisterModel {
    userName: string;
    password: string;
    rememberMe:boolean=false;
}
</code></pre>
<pre><code>import { RegisterModel } from './model/register-model';

export class FormQuickStartComponent implements OnInit {
  public regModel:RegisterModel=new RegisterModel();
}
</code></pre>
<h3 id="-1">状态标志位</h3>
<p>Form、FormGroup、FormControl（输入项）都有一些标志位可以使用，这些标志位是 Angular 提供的，一共有 9 个（官方的文档里面没有明确列出来，或者列得不全）：</p>
<ul>
<li>valid，校验成功</li>
<li>invalid，校验失败</li>
<li>pending，表单正在提交过程中</li>
<li>pristine，数据依然处于原始状态，用户没有修改过</li>
<li>dirty，数据已经变脏了，被用户改过了</li>
<li>touched，被触摸或者单击过</li>
<li>untouched，未被触摸或者单击</li>
<li>enabled，启用状态</li>
<li>disabled，禁用状态</li>
</ul>
<p>Form 上面多一个状态标志位 submitted，可以用来判断表单是否已经被提交。</p>
<p>我们可以利用这些标志位来判断表单和输入项的状态。</p>
<h3 id="-2">内置校验规则</h3>
<p>Angular 一共内置了 8 种校验规则：</p>
<ul>
<li>required</li>
<li>requiredTrue</li>
<li>minLength</li>
<li>maxLength</li>
<li>pattern</li>
<li>nullValidator</li>
<li>compose</li>
<li>composeAsync</li>
</ul>
<p><a href="https://angular.io/api/forms/Validators">详细的 API 描述可参见这里</a>。</p>
<h3 id="-3">自定义校验规则</h3>
<p>内置的校验规则经常不够用，尤其在需要多条件联合校验的时候，因此我们需要自己定义校验规则。</p>
<p>请看这个例子：</p>
<p><img width="50%" src="https://images.gitbook.cn/72d9b080-f381-11e8-aeb7-01d6aed3aa05"></p>
<p>关键 HTML 模板代码：</p>
<pre>
&lt;div class="form-group"  [ngClass]="{'has-error': mobile.invalid && (mobile.dirty || mobile.touched) }"&gt;
  &lt;label class="col-xs-2 control-label"&gt;手机号：&lt;/label&gt;
  &lt;div class="col-xs-10"&gt;
    &lt;input #mobile="ngModel" [(ngModel)]="regModel.mobile" name="mobile" ChineseMobileValidator class="form-control" placeholder="Mobile"&gt;
    &lt;div *ngIf="mobile.invalid && (mobile.dirty || mobile.touched)" class="text-danger"&gt;
        &lt;div *ngIf="!mobile.errors.ChineseMobileValidator"&gt;
          请输入合法的手机号
        &lt;/div&gt;
    &lt;/div&gt;
  &lt;/div&gt;
&lt;/div&gt;
</pre>
<p>自定义的校验规则代码：</p>
<pre><code>import { Directive, Input } from '@angular/core';
import { Validator, AbstractControl, NG_VALIDATORS } from '@angular/forms';


@Directive({
    selector: '[ChineseMobileValidator]',
    providers: [
        {
            provide: NG_VALIDATORS,
            useExisting: ChineseMobileValidator,
            multi: true
        }
    ]
})
export class ChineseMobileValidator implements Validator {
    @Input() ChineseMobileValidator: string;

    constructor() { }

    validate(control: AbstractControl): { [error: string]: any } {
        let val = control.value;        
        let flag=/^1(3|4|5|7|8)\d{9}$/.test(val);
        console.log(flag);
        if(flag){
            control.setErrors(null);
            return null
        }else{
            control.setErrors({ChineseMobileValidator:false});
            return {ChineseMobileValidator:false};
        }
    }
}
</code></pre>
<p>可以看到，自定义校验规则的使用方式和内置校验规则并没有什么区别。</p>
<p>当然，也可以把正则表达式传给内置的 pattern 校验器来实现这个效果，但是每次都复制正则比较麻烦，对于你的业务系统常见的校验规则，还是把它沉淀成你们自己的校验规则库可复用性更高。</p>
<p><a href="https://gitee.com/learn-angular-series/learn-form">本课完整可运行的代码可参见这里</a>，代码在 validation 分支上。</p>
<p><a href="https://angular.io/api/forms/Validators">关于校验器更详细的 API 描述参见这里</a>。</p></div></article>